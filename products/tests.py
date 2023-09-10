from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class IndexListViewTestCase(TestCase):
    # TEST FOR MAIN PAIG 
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK) # Check status code
        self.assertEqual(response.context['title'], 'AppleRedStore - Home') # Check title 
        self.assertTemplateUsed(response, 'products/index.html') # Test template name


class ProductsListViewTestCase(TestCase):
    # TEST FOR MAIN PAIG 
    def test_view(self):
        path = reverse('products:catalog')
        # Accept a response from the website
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK) # Check status code
        self.assertEqual(response.context['title'], 'AppleRedStore - Catalog') # Check title 
        self.assertTemplateUsed(response, 'products/catalog.html') # Test template name
