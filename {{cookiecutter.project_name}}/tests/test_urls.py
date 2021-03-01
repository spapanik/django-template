from django.test import Client


def test_admin():
    client = Client()
    response = client.get("/admin", follow=True)
    expected_redirects = [("/admin/", 301), ("/admin/login/?next=/admin/", 302)]
    assert response.redirect_chain == expected_redirects
