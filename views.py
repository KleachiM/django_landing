from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_land = request.GET['from-landing']
    counter_click[from_land] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    arg = request.GET['ab-test-arg']
    if arg == 'original':
        temp_path = 'landing.html'
        counter_show[arg] += 1
    elif arg == 'test':
        temp_path = 'landing_alternate.html'
        counter_show[arg] += 1
    return render(request, temp_path)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': counter_click['test']/counter_show['test'] if counter_show['test'] else 0,
        'original_conversion': counter_click['original']/counter_show['original'] if counter_show['original'] else 0,
    })
