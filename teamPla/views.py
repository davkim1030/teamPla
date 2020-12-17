from django.shortcuts import render, redirect


def main(request):
    return render(request, 'main.html')


def register_team(request):
    request.META['Bearer'] = "298a9ead836455ebcfd8dcc75c7872117532d055fbfb460580052d67c6f06dea"
    return redirect("https://api.intra.42.fr/v2/users/hyukim")


def pending_team(request):
    return render(request, 'pending_team.html')


def team_info(request):
    return render(request, 'team_info.html')

