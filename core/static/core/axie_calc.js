const axieCard = document.getElementsByClassName('axie-card');
const axieCardSelected = document.getElementsByClassName('axie-card-selected');
const targetClass = document.getElementsByName('target-class');
const resetButton = document.getElementById('reset-btn');
const cardsSelected = document.getElementById('cards-selected');
const damageOutput = document.getElementById('damage-output');


for (var i = 0; i < axieCard.length; i++) {
    axieCard[i].addEventListener('click', updateDamage);
}

for (var i = 0; i < targetClass.length; i++) {
    targetClass[i].onclick = updateDamage;
}

resetButton.addEventListener('click', reset);

function updateDamage() {

    let cards = [];

    for (var i = 0; i < axieCardSelected.length; i++) {
        cards.push({
            'axie_id': axieCardSelected[i].getAttribute('data-axie-id'),
            'part_name': axieCardSelected[i].getAttribute('data-part-name'),
            'img_src': axieCardSelected[i].getAttribute('src'),
        });
    }

    if (this.value == undefined) {
        cards.push({
            'axie_id': this.getAttribute('data-axie-id'),
            'part_name': this.getAttribute('data-part-name'),
            'img_src': this.getAttribute('src'),
        });
    }

    let targetClassVal = 0;
    for (var i = 0, length = targetClass.length; i < length; i++) {
        if (targetClass[i].checked) {
            targetClassVal = targetClass[i].value;
            console.log(targetClassVal);
            break;
        }
    }

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('selected_cards', JSON.stringify(cards));
    formData.append('target_class', targetClassVal);

    fetch(updateDamageUrl, {
        method: 'POST',
        body: formData,
    }).then(response => response.json()).then(result => {
        updateSelectedCards(result);
    });
}

function updateSelectedCards(result) {
    cardsSelected.innerHTML = result.html;
    damageOutput.innerHTML = result.damage_output;
}

function reset() {
    cardsSelected.innerHTML = '';
    damageOutput.innerHTML = 0;
}

