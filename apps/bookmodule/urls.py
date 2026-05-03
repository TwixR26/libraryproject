from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    
    
    path('html5/links/', views.links, name="books.links"),
    path('html5/text/formatting/', views.formatting, name="books.formatting"),
    path('html5/listing/', views.listing, name="books.listing"),
    path('html5/tables/', views.tables, name="books.tables"),
    path('search/', views.search, name="books.search"),
    path('simple/query/', views.simple_query, name="books.simple_query"),
    path('complex/query/', views.complex_query, name="books.complex_query"),
    path('lab8/task1', views.task1, name="books.task1"),
    path('lab8/task2', views.task2, name="books.task2"),
    path('lab8/task3', views.task3, name="books.task3"),
    path('lab8/task4', views.task4, name="books.task4"),
    path('lab8/task5', views.task5, name="books.task5"),
    path('lab8/task7', views.task7, name="books.task7"),
    path('lab9/task1', views.task1_lab9, name="lab9.task1"),
    path('lab9/task2', views.task2_lab9, name="lab9.task2"),
    path('lab9/task3', views.task3_lab9, name="lab9.task3"),
    path('lab9/task4', views.task4_lab9, name="lab9.task4"),
    path('lab9/task5', views.task5_lab9, name="lab9.task5"),
    path('lab9/task6', views.task6_lab9, name="lab9.task6"),
    path('lab9_part1/listbooks', views.listbooks_part1, name='lab10_part1.list'),
    path('lab9_part1/addbook', views.addbook_part1, name='lab10_part1.add'),
    path('lab9_part1/editbook/<int:id>', views.editbook_part1, name='lab10_part1.edit'),
    path('lab9_part1/deletebook/<int:id>', views.deletebook_part1, name='lab10_part1.delete'),
    path('lab9_part2/listbooks', views.listbooks_part2, name='lab10_part2.list'),
    path('lab9_part2/addbook', views.addbook_part2, name='lab10_part2.add'),
    path('lab9_part2/editbook/<int:id>', views.editbook_part2, name='lab10_part2.edit'),
    path('lab9_part2/deletebook/<int:id>', views.deletebook_part2, name='lab10_part2.delete'),
]