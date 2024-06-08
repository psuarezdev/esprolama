from django.db import models


class Strategy(models.Model):
    class Meta:
        verbose_name_plural = 'Strategies'

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Principle(models.Model):
    # This principle_id it's going to be used just for the order of the principles
    principle_id = models.IntegerField()
    title = models.CharField(max_length=255)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    def __str__(self):
        return f'Strategy {self.strategy.id} - Principle {self.principle_id}'


class Descriptor(models.Model):
    # This descriptor_id it's going to be used just for the order of the descriptors
    descriptor_id = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Individual(models.Model):
    answer = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    user_id = models.IntegerField()
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.strategy.id}.{self.principle.id}.{self.descriptor.id} - {self.answer}'
