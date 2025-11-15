from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from io import BytesIO
from .models import Resume
from rest_framework import generics
from .serializers import PostSerializer

def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("PDF generation error", status=500)

def export_resume_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    context = {'resume': resume}
    return render_to_pdf('resumes/pdf_template.html', context)

class PostListApi(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer