from django.db import models


class Strategy(models.Model):
    class Meta:
        verbose_name_plural = 'Strategies'

    title = models.CharField(max_length=255)

    def __str__(self):
        return f'Strategy {self.id}'


class Principle(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    # This principle_id it's going to be used just for the order of the principles
    principle_id = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'Strategy {self.strategy.id} - Principle {self.principle_id}'


class Descriptor(models.Model):
    # This descriptor_id it's going to be used just for the order of the descriptors
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE)
    descriptor_id = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'Strategy {self.strategy.id} - Principle {self.principle.principle_id} - Descriptor {self.descriptor_id}'


class Individual(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    answer = models.IntegerField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        # TODO: Add the username
        return f'Strategy {self.strategy.id} - Principle {self.principle.principle_id} - Descriptor {self.descriptor.descriptor_id} - Answer {self.answer}'
