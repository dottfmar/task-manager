from django.test import TestCase
from django.urls import reverse
from tasks.models import Team, Project, Task, TaskType
from django.contrib.auth import get_user_model


class HomePageViewTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/home.html")


class ProfileViewTest(TestCase):
    def test_profile_view_logged_in(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("tasks:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/my_profile.html")

    def test_profile_view_not_logged_in(self):
        response = self.client.get(reverse("tasks:profile"))
        self.assertRedirects(response, "/accounts/login/?next=/profile/")


class EditProfileViewTest(TestCase):
    def test_edit_profile_view(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("tasks:edit-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_form.html")


class TaskViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Створення кількох задач
        self.task1 = Task.objects.create(
            name="Task 1",
            description="Description of Task 1",
            is_completed=True,
            priority="HIGH",
        )
        self.task2 = Task.objects.create(
            name="Task 2",
            description="Description of Task 2",
            is_completed=False,
            priority="MEDIUM",
        )
        self.task3 = Task.objects.create(
            name="Task 3",
            description="Description of Task 3",
            is_completed=True,
            priority="LOW",
        )

    def test_filter_by_completed_true(self):
        response = self.client.get(reverse("tasks:tasks") + "?completed=true")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task1, response.context["object_list"])
        self.assertIn(self.task3, response.context["object_list"])
        self.assertNotIn(self.task2, response.context["object_list"])

    def test_filter_by_completed_false(self):
        response = self.client.get(reverse("tasks:tasks") + "?completed=false")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task2, response.context["object_list"])
        self.assertNotIn(self.task1, response.context["object_list"])
        self.assertNotIn(self.task3, response.context["object_list"])

    def test_filter_by_priority(self):
        response = self.client.get(reverse("tasks:tasks") + "?priority=HIGH")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task1, response.context["object_list"])
        self.assertNotIn(self.task2, response.context["object_list"])
        self.assertNotIn(self.task3, response.context["object_list"])

    def test_filter_by_multiple_params(self):
        response = self.client.get(
            reverse("tasks:tasks") + "?completed=true&priority=HIGH"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task1, response.context["object_list"])
        self.assertNotIn(self.task2, response.context["object_list"])
        self.assertNotIn(self.task3, response.context["object_list"])

    def test_no_filters(self):
        response = self.client.get(reverse("tasks:tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.task1, response.context["object_list"])
        self.assertIn(self.task2, response.context["object_list"])
        self.assertIn(self.task3, response.context["object_list"])


class TeamCreateViewTest(TestCase):
    def test_team_create_view(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        user_id = user.id
        data = {
            "name": "Team A",
            "description": "Description of Team A",
            "members": [user_id],
        }
        response = self.client.post(reverse("tasks:team-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:teams"))
        self.assertTrue(Team.objects.filter(name="Team A").exists())


class TaskToggleStatusViewTest(TestCase):
    def test_toggle_task_status(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            name="Test Task", description="Test Description", is_completed=False
        )
        response = self.client.post(
            reverse("tasks:task-toggle-status", kwargs={"pk": task.pk})
        )
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        self.assertRedirects(response, reverse("tasks:tasks"))


class TaskCreateViewTest(TestCase):
    def test_create_task(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        team = Team.objects.create(name="Team A")
        project = Project.objects.create(
            name="Project A", description="Project A Description", team=team
        )

        task_type = TaskType.objects.create(name="Bug")
        priority = "HIGH"
        assignees = [user.id]
        data = {
            "name": "Test Task",
            "description": "Task Description",
            "deadline": "2025-02-10T10:00:00",
            "priority": priority,
            "task_type": task_type.id,
            "project": project.id,
            "assignees": assignees,
        }
        response = self.client.post(reverse("tasks:task-create"), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))
        self.assertTrue(Task.objects.filter(name="Test Task").exists())
        task = Task.objects.get(name="Test Task")
        self.assertTrue(task.assignees.filter(id=user.id).exists())


class TaskUpdateViewTest(TestCase):
    def test_update_task(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Створюємо команду, проект і тип задачі
        team = Team.objects.create(name="Team A")
        project = Project.objects.create(
            name="Project A", description="Project A Description", team=team
        )
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="Test Task",
            description="Task Description",
            is_completed=False,
            project=project,
            task_type=task_type,
        )
        data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "is_completed": True,
            "priority": "HIGH",
            "task_type": task_type.id,
            "project": project.id,
            "assignees": [user.id],
        }
        response = self.client.post(
            reverse("tasks:task-update", kwargs={"pk": task.pk}), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Task")
        self.assertEqual(task.description, "Updated Description")
        self.assertTrue(task.is_completed)


class TaskDeleteViewTest(TestCase):
    def test_delete_task(self):
        user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            name="Test Task", description="Task Description", is_completed=False
        )
        response = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:tasks"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
