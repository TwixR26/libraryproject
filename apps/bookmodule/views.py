from django.shortcuts import render
from .models import Book
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Address, Student
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Publisher, Author

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


def links(request):
    return render(request, 'bookmodule/links.html')

def formatting(request):
    return render(request, 'bookmodule/formatting.html')

def listing(request):
    return render(request, 'bookmodule/listing.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower(): contained = True
            
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    
    return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
def task1(request):
    mybooks = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task2(request):
    mybooks = Book.objects.filter(Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task3(request):
    mybooks = Book.objects.filter(~Q(edition__gt=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})
def task4(request):
    mybooks = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})

def task7(request):
    city_counts = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/task7.html', {'city_counts': city_counts})

def task1_lab9(request):
    books = Book.objects.all()
    
    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total'] or 1
    
    for book in books:
        book.percentage = round((book.quantity / total_quantity) * 100, 2)
        
    return render(request, 'bookmodule/lab9_task1.html', {'books': books})

def task2_lab9(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})

def task3_lab9(request):
    publishers = Publisher.objects.annotate(oldest_book=Min('book__pubdate'))
    return render(request, 'bookmodule/lab9_task3.html', {'publishers': publishers})

def task4_lab9(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})

def task5_lab9(request):
    publishers = Publisher.objects.annotate(
        highly_rated=Count('book', filter=Q(book__rating__gte=4))
    )
    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})

def task6_lab9(request):
    publishers = Publisher.objects.annotate(
        filtered_books=Count('book', filter=Q(book__price__gt=50, book__quantity__gte=1, book__quantity__lt=5))
    )
    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})