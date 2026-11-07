from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.decorators import role_required
from accounts.models import User
from .forms import CaseForm
from .models import Case


def home(request):
    if request.user.is_authenticated:
        return redirect("cases:list")
    return redirect("login")


@role_required(User.Role.REQUESTER, User.Role.AUDITOR, User.Role.SUPERUSER)
def case_list(request):
    role = request.user.role
    is_privileged = role in (User.Role.AUDITOR, User.Role.SUPERUSER)
    queryset = Case.objects.select_related("requester").order_by("-created_at")

    if not is_privileged:
        queryset = queryset.filter(Q(requester=request.user) | Q(is_public=True))

    rows = []
    map_cases = []
    for case in queryset:
        can_view_detail = is_privileged or case.requester_id == request.user.id
        detail_url = reverse("cases:detail", args=[case.pk]) if can_view_detail else ""
        rows.append({
            "case": case,
            "can_view_detail": can_view_detail,
            "detail_url": detail_url,
        })
        map_cases.append({
            "latitude": float(case.latitude),
            "longitude": float(case.longitude),
            "title": case.title if can_view_detail else "Chamado p\u00fablico",
            "status": case.get_status_display(),
            "detail_url": detail_url,
        })

    return render(request, "cases/case_list.html", {
        "cases": rows,
        "map_cases": map_cases,
        "is_privileged": is_privileged,
        "can_create": role in (User.Role.REQUESTER, User.Role.SUPERUSER),
    })


@role_required(User.Role.REQUESTER, User.Role.SUPERUSER)
def case_create(request):
    form = CaseForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        case = form.save(commit=False)
        case.requester = request.user
        case.save()

        messages.success(request, "Chamado registrado com sucesso.")
        return redirect("cases:detail", pk=case.pk)

    return render(request, "cases/case_form.html", {"form": form})


@role_required(User.Role.REQUESTER, User.Role.AUDITOR, User.Role.SUPERUSER)
def case_detail(request, pk):
    case = get_object_or_404(Case.objects.select_related("requester"), pk=pk)
    role = request.user.role

    if role == User.Role.REQUESTER:
        if case.requester_id == request.user.id:
            return render(request, "cases/case_detail.html", {
                "case": case,
                "is_privileged": False,
            })
        if case.is_public:
            return render(request, "cases/public_status.html", {
                "public_id": case.pk,
                "status": case.get_status_display(),
            })
        raise Http404

    if role in (User.Role.AUDITOR, User.Role.SUPERUSER):
        return render(request, "cases/case_detail.html", {
            "case": case,
            "is_privileged": True,
        })

    raise PermissionDenied