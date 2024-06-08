from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Strategy, Principle, Descriptor, Individual


def new_individual(request: HttpRequest):
    strategies = Strategy.objects.all()
    return render(request, 'elama/new_individual.html', {'strategies': strategies})


def new_individual_principles(request: HttpRequest, strategy_id: int):
    principles = Principle.objects.filter(strategy_id=strategy_id)
    return render(request, 'elama/new_individual_principles.html', {
        'strategy_id': strategy_id,
        'principles': principles
    })


def new_individual_descriptor(request: HttpRequest, strategy_id: int, principle_id: int, descriptor_id: int):
    previous_principle = principle_id
    previous_descriptor = descriptor_id - 1
    next_descriptor = descriptor_id + 1

    if previous_descriptor == 0:
        last_descriptor = Descriptor.objects.filter(
            strategy_id=strategy_id, principle_id__lt=principle_id
        ).last()

        if last_descriptor is not None:
            previous_principle = last_descriptor.principle_id
            previous_descriptor = last_descriptor.descriptor_id

    last_principle_descriptor = Descriptor.objects.filter(strategy_id=strategy_id, principle_id=principle_id).last()
    if next_descriptor > last_principle_descriptor.descriptor_id:
        next_principle = Principle.objects.filter(strategy_id=strategy_id, principle_id__gt=principle_id).first()

        if next_principle is not None:
            principle_id = next_principle.principle_id
            first_descriptor = Descriptor.objects.filter(strategy_id=strategy_id, principle_id=principle_id).first()
            next_descriptor = first_descriptor.descriptor_id if first_descriptor is not None else 1

    if request.method == 'POST':
        answer = request.POST['answer'] if 'answer' in request.POST else None

        if answer is None:
            return redirect('new_individual_principles', strategy_id=strategy_id)

        individual = Individual.objects.filter(
            user_id=1,  # TODO: Change this to the authenticated user
            strategy_id=strategy_id,
            principle_id=previous_principle,
            descriptor_id=previous_descriptor,
        ).first()

        if individual is not None and individual.answer != answer:
            individual.answer = answer
            individual.save()
        elif individual is None:
            Individual(
                answer=answer,
                user_id=1,  # TODO: Change this to the authenticated user
                strategy_id=strategy_id,
                principle_id=previous_principle,
                descriptor_id=previous_descriptor,
            ).save()

        last_principle = Principle.objects.filter(strategy_id=strategy_id).last()
        last_descriptor = Descriptor.objects.filter(principle_id=last_principle.principle_id).last()

        if previous_principle == last_principle.principle_id and previous_descriptor == last_descriptor.descriptor_id:
            Individual.objects.filter(
                user_id=1,  # TODO: Change this to the authenticated user
                strategy_id=strategy_id,
            ).update(confirmed=True)

            return redirect('new_individual')

    descriptor = get_object_or_404(
        Descriptor, strategy_id=strategy_id, principle_id=principle_id, descriptor_id=descriptor_id
    )
    selected_answer = Individual.objects.filter(
        user_id=1, strategy_id=strategy_id, principle_id=principle_id, descriptor_id=descriptor_id,
    ).first()

    return render(request, 'elama/new_individual_descriptor.html', {
        'strategy_id': strategy_id,
        'principle_id': principle_id,
        'descriptor': descriptor,
        'selected_answer': selected_answer,
        'previous_principle': previous_principle,
        'previous_descriptor': previous_descriptor,
        'next_descriptor': next_descriptor,
    })
