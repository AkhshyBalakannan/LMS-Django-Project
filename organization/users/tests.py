from django.http import response
from django.test import TestCase, Client
from .models import CustomUser
from leavemanagementsys.models import LeaveRequest
from django.urls import reverse


class UserCreationsTestCase(TestCase):
    '''This class is to test whether an user can be cerated
    with no bugs'''

    def test_create_user(self):
        '''This method will create an instance of users employee and manager'''
        manager_user = CustomUser.objects.create(username='testuser_m', first_name='test', last_name='user',
                                                 email='testuser_m@gm.com',
                                                 password='passwordtestingacc', is_employee=True,
                                                 is_manager=True, leave_eligible=12, leave_taken=0, leave_remaining=12, lop_leave_taken=0,
                                                 covid_leave_taken=0)

        employee_user = CustomUser.objects.create(username='testuser_e', first_name='test', last_name='user',
                                                  email='testuser_m@gm.com', password='passwordtestingacc', is_employee=True,
                                                  is_manager=False, leave_eligible=12, leave_taken=0, leave_remaining=12, lop_leave_taken=0,
                                                  covid_leave_taken=0)

        manager_user = CustomUser.objects.get(username='testuser_m')
        employee_user = CustomUser.objects.get(username='testuser_e')

        self.assertEqual(manager_user.username, 'testuser_m')
        self.assertEqual(employee_user.username, 'testuser_e')

    def test_leave_request_create(self):
        logged_user = CustomUser.objects.get_or_create(
            username='testuser_e', password='passwordtestingacc')
        c = Client()
        logged_user.CustomUser
        logged_in = c.login(username='testuser_e',
                            password='passwordtestingacc')
        leave_request = LeaveRequest.objects.create(applied_user=logged_user,
                                                    description="Leave from testing", from_date=10-10-2021, to_date=22-10-2021, leave_type='Personal', number_of_days=12)
        leave_request.save()

        self.assertTrue(logged_in)
        self.assertEqual(leave_request, 'Leave from testing')

    def test_user_profile_with_leave_history(self):
        # '''This method is to get the profile page'''
        client = Client()

        login = self.client.login(
            username='testuser_e', password='passwordtestingacc')

        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)

    def test_request_leave(self):
        '''This method is to request for leave'''
        pass
