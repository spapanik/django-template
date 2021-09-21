def test_admin(http_client):
    response = client.get("/admin", follow=True)
    expected_redirects = [("/admin/", 301), ("/admin/login/?next=/admin/", 302)]
    assert response.redirect_chain == expected_redirects
