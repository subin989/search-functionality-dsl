from rest_framework import viewsets
from django.http import JsonResponse
# from django_elasticsearch_dsl.search import Search
from .models import Book
from .documents import BookDocument


class AddBookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        author = request.data.get("author")

        book = Book.objects.create(
            title=title,
            author=author,
        )

        return JsonResponse(
            {"message": "Book added successfully", "book_id": book.id}, status=201
        )

    def list(self, request, *args, **kwargs):
        books = Book.objects.all()
        book_data = [
            {
                "title": book.title,
                "author": book.author,
            }
            for book in books
        ]

        return JsonResponse({"books": book_data}, safe=False)

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        book_data = {
            "title": book.title,
            "author": book.author,
        }

        return JsonResponse(book_data)


class SearchView(viewsets.ViewSet):
    def list(self, request):
        q = request.query_params.get("q", "")
        print("Query", q)
        s = BookDocument.search().query("match", author=q)
        results = s.execute()

        search_results = [
            {
                "title": hit.title,
                "author": hit.author,
            }
            for hit in results
        ]

        return JsonResponse({"results": search_results})
