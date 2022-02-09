from django.db import models
from users.models import Ronin


class Axie(models.Model):
    axie_id = models.PositiveBigIntegerField()
    ronin = models.ForeignKey(Ronin, on_delete=models.CASCADE, related_name='axies')
    info = models.JSONField()

    hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.axie_id)

    @property
    def name(self):
        return self.info['axie']['name']

    @property
    def class_(self):
        return self.info['axie']['class']

    @property
    def parts(self):
        parts = self.info['axie']['parts'][2:]
        return parts

    @property
    def stats(self):
        stats = self.info['axie']['stats']
        del stats['__typename']

        return stats

    @property
    def image(self):
        return self.info['axie']['image']

    def get_ability_details(self, part_name):
        for part in self.parts:
            if part['name'] == part_name:
                details = part['abilities'][0]
                details['class'] = part['class']
                return details

        raise ValueError(f'{part_name} is not found.')