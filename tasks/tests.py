from django.test import TestCase
from django.urls import reverse
from .models import Task
from .forms import TaskForm

class TaskModelTest(TestCase):
    def test_task_str(self):
        task = Task.objects.create(title='Тестовая задача')
        self.assertEqual(str(task), 'Тестовая задача')
        self.assertFalse(task.is_completed)

class TaskViewsTest(TestCase):
    def setUp(self):
        self.task1 = Task.objects.create(title='Задача 1', description='Описание 1')
        self.task2 = Task.objects.create(title='Задача 2', description='Описание 2', is_completed=True)

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 2')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Описание 1')

    def test_task_create_get(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_post_valid(self):
        response = self.client.post(reverse('task_create'), {'title': 'Новая задача', 'description': 'Новое описание'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Новая задача').exists())

    def test_task_toggle_status(self):
        self.assertFalse(self.task1.is_completed)
        response = self.client.post(reverse('task_toggle', args=[self.task1.pk]))
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)

        response = self.client.post(reverse('task_toggle', args=[self.task1.pk]))
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_completed)

class TaskFormTest(TestCase):
    def test_form_validation(self):
        form = TaskForm(data={'title': '', 'description': 'Без названия'})
        self.assertFalse(form.is_valid())

        form = TaskForm(data={'title': 'С названием'})
        self.assertTrue(form.is_valid())
