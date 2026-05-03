from django.shortcuts import render
from .models import Book
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Address, Student
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Publisher, Author
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import BookForm
from .models import Book, Address, Student, Publisher, Author
from .forms import BookForm, StudentForm
from .forms import Student2Form
from .models import Student2
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

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

def listbooks_part1(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab10_part1_list.html', {'books': books})


def addbook_part1(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
       
        Book.objects.create(
            title=title, 
            price=float(price), 
            quantity=int(quantity), 
            pubdate=timezone.now()
        )
        return redirect('lab10_part1.list') 
    return render(request, 'bookmodule/lab10_part1_add.html')


def editbook_part1(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.price = float(request.POST.get('price'))
        book.quantity = int(request.POST.get('quantity'))
        book.save()
        return redirect('lab10_part1.list')
        
    return render(request, 'bookmodule/lab10_part1_edit.html', {'book': book})


def deletebook_part1(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('lab10_part1.list')

def listbooks_part2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab10_part2_list.html', {'books': books})

def addbook_part2(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.pubdate = timezone.now() 
            book.save()
            return redirect('lab10_part2.list')
    else:
        form = BookForm()
    return render(request, 'bookmodule/lab10_part2_add.html', {'form': form})

def editbook_part2(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('lab10_part2.list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/lab10_part2_edit.html', {'form': form, 'book': book})

def deletebook_part2(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('lab10_part2.list')

def list_students(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/lab11_task1_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab11_task1.list')
    else:
        form = StudentForm()
    return render(request, 'bookmodule/lab11_task1_add.html', {'form': form})

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('lab11_task1.list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'bookmodule/lab11_task1_edit.html', {'form': form, 'student': student})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('lab11_task1.list')
@login_required(login_url='/users/login')
def list_students2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/lab11_task2_list.html', {'students': students})
@login_required(login_url='/users/login')
def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab11_task2.list')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/lab11_task2_add.html', {'form': form})

def edit_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('lab11_task2.list')
    else:
        form = Student2Form(instance=student)
    return render(request, 'bookmodule/lab11_task2_edit.html', {'form': form, 'student': student})

def delete_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    student.delete()
    return redirect('lab11_task2.list')

def list_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'bookmodule/lab11_task3_list.html', {'profiles': profiles})

def add_profile(request):
    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lab11_task3.list')
    else:
        form = UserProfileForm()
    return render(request, 'bookmodule/lab11_task3_add.html', {'form': form})