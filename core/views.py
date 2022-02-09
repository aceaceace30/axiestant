import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from core.axie_api import AxieAPI
from core.calculations import calculate_damage, AXIE_GROUP
from core.forms import RoninForm
from core.models import Axie
from users.models import Ronin


def main(request):
    template_name = 'core/main.html'

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    try:
        ronin_obj = Ronin.objects.get(session_id=session_key)
    except (Ronin.DoesNotExist, Ronin.MultipleObjectsReturned):
        ronin_obj = None

    if request.method == 'POST':
        form = RoninForm(request.POST, instance=ronin_obj)
        if form.is_valid():
            ronin = form.save(commit=False)
            ronin.session_id = session_key
            ronin.save()

            axie_api = AxieAPI(ronin.address)
            axie_ids = axie_api.get_axie_ids()

            axies_create = list()
            for axie_id in axie_ids:
                try:
                    axie_data = axie_api.get_axie(axie_id)
                    axie = Axie(axie_id=axie_data['axie']['id'], ronin=ronin, info=axie_data)
                    axies_create.append(axie)
                except Exception as e:
                    print(str(e))

            Axie.objects.filter(ronin=ronin).delete()
            Axie.objects.bulk_create(axies_create)

            return redirect('main')
    else:
        form = RoninForm()

    axie_group = dict()
    for num, axie_list in AXIE_GROUP.items():
        axie_group[num] = '/'.join(axie_list)

    q_filter = {'ronin': ronin_obj}
    hidden = request.GET.get('hidden')
    if hidden == 'True':
        q_filter['hidden'] = True
    elif hidden == 'False':
        q_filter['hidden'] = False

    axies = Axie.objects.filter(**q_filter)

    context = {
        'form': form,
        'axies': axies,
        'axie_group': axie_group,
    }

    return render(request, template_name, context)


@require_POST
def update_damage(request):
    selected_cards = json.loads(request.POST['selected_cards'])
    target_class = int(request.POST['target_class'])
    context = {'selected_cards': selected_cards}

    card_count_per_axie = dict()
    for item in selected_cards:
        if item['axie_id'] not in card_count_per_axie:
            card_count_per_axie[item['axie_id']] = 1
        else:
            card_count_per_axie[item['axie_id']] += 1

    damage_output,attack_up_current_multiplier = (0, 0)
    for item in selected_cards:
        axie = Axie.objects.get(axie_id=item['axie_id'])
        card_count = card_count_per_axie[item['axie_id']]
        calculated_damage, attack_up_current_multiplier = calculate_damage(axie=axie,
                                                                           target_class=target_class,
                                                                           part_name=item['part_name'],
                                                                           card_count=card_count,
                                                                           attack_up_current_multiplier=attack_up_current_multiplier)
        damage_output += calculated_damage
        item['calculated_damage'] = calculated_damage

    html = render_to_string('core/snippets/axie_selected_cards.html', context)

    return JsonResponse({'html': html, 'damage_output': damage_output})


def toggle_hidden_axie(request, axie_id):
    try:
        ronin = Ronin.objects.get(session_id=request.session.session_key)
        axie = ronin.axies.get(axie_id=axie_id)
        axie.hidden = not axie.hidden
        axie.save()
    except Ronin.DoesNotExist:
        pass

    return redirect('main')
