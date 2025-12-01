from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoTests(TestCase):

    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test Description",
            due_date="2025-12-31",
            is_resolved=False
        )

    def test_create_todo(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'New TODO',
            'description': 'New Description',
            'due_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)

    def test_edit_todo(self):
        response = self.client.post(reverse('todo_update', args=[self.todo.id]), {
            'title': 'Updated TODO',
            'description': 'Updated Description',
            'due_date': '2025-12-31',
            'is_resolved': True
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated TODO')
        self.assertTrue(self.todo.is_resolved)

    def test_delete_todo(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_list_todos(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)

    def test_todo_detail(self):
        response = self.client.get(reverse('todo_detail', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)
