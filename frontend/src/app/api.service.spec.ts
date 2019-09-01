import { TestBed, getTestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { ApiService } from './api.service';

describe('ApiService', () => {
  let injector: TestBed;
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService]
    });
    injector = getTestBed();
    service = injector.get(ApiService);
    httpMock = injector.get(HttpTestingController);
  });

  describe('#getCategoriesWithProducts', () => {
    it('should return a list of categories', () => {
      const categories = [
        { name: 'Category1', products: [] },
        { name: 'Category2', products: [] }
      ];

      service.getCategoriesWithProducts().subscribe(data => {
        expect(data.length).toBe(2);
        expect(data).toEqual(categories);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories?products=1');
      expect(req.request.method).toBe('GET');
      req.flush(categories);
      httpMock.verify();
    });
  });

  describe('#getCategories', () => {
    it('should return a list of categories', () => {
      const categories = [
        { name: 'Category1' },
        { name: 'Category2' }
      ];

      service.getCategories().subscribe(data => {
        expect(data.length).toBe(2);
        expect(data).toEqual(categories);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories');
      expect(req.request.method).toBe('GET');
      req.flush(categories);
      httpMock.verify();
    });
  });

  describe('#getCategoryWithProducts', () => {
    it('should return a category', () => {
      const id = '100';
      const category = { name: 'Category1', products: [] };

      service.getCategoryWithProducts(id).subscribe(data => {
        expect(data).toEqual(category);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories/' + id + '?products=1');
      expect(req.request.method).toBe('GET');
      req.flush(category);
      httpMock.verify();
    });
  });

  describe('#getCategory', () => {
    it('should return a category', () => {
      const id = '100';
      const category = { name: 'Category1' };

      service.getCategory(id).subscribe(data => {
        expect(data).toEqual(category);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories/' + id);
      expect(req.request.method).toBe('GET');
      req.flush(category);
      httpMock.verify();
    });
  });

  describe('#createCategory', () => {
    it('should return a category', () => {
      const category = { name: 'Category1' };

      service.createCategory(category).subscribe(data => {
        expect(data.name).toEqual(category.name);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories');
      expect(req.request.method).toBe('POST');
      req.flush(category);
      httpMock.verify();
    });
  });

  describe('#updateCategory', () => {
    it('should return a category', () => {
      const id = '100';
      const category = { name: 'Category1' };

      service.updateCategory(id, category).subscribe(data => {
        expect(data.name).toEqual(category.name);
      });

      const req = httpMock.expectOne(service.baseURL + 'categories/' + id);
      expect(req.request.method).toBe('PUT');
      req.flush(category);
      httpMock.verify();
    });
  });

  describe('#deleteCategory', () => {
    it('test delete category', () => {
      const id = '100';

      service.deleteCategory(id).subscribe();

      const req = httpMock.expectOne(service.baseURL + 'categories/' + id);
      expect(req.request.method).toBe('DELETE');
      req.flush({});
      httpMock.verify();
    });
  });

  describe('#getProductsWithCategories', () => {
    it('should return a list of products', () => {
      const products = [
        { name: 'Product1', price: 10, categories: [] },
        { name: 'Product2', price: 100, categories: [] }
      ];

      service.getProductsWithCategories().subscribe(data => {
        expect(data.length).toBe(2);
        expect(data).toEqual(products);
      });

      const req = httpMock.expectOne(service.baseURL + 'products?categories=1');
      expect(req.request.method).toBe('GET');
      req.flush(products);
      httpMock.verify();
    });
  });

  describe('#getProducts', () => {
    it('should return a list of products', () => {
      const products = [
        { name: 'Product1', price: 10 },
        { name: 'Product2', price: 100 }
      ];

      service.getProducts().subscribe(data => {
        expect(data.length).toBe(2);
        expect(data).toEqual(products);
      });

      const req = httpMock.expectOne(service.baseURL + 'products');
      expect(req.request.method).toBe('GET');
      req.flush(products);
      httpMock.verify();
    });
  });

  describe('#getProductWithCategories', () => {
    it('should return a product', () => {
      const id = '100';
      const product = { name: 'Product1', price: 100, categories: [] };

      service.getProductWithCategories(id).subscribe(data => {
        expect(data).toEqual(product);
      });

      const req = httpMock.expectOne(service.baseURL + 'products/' + id + '?categories=1');
      expect(req.request.method).toBe('GET');
      req.flush(product);
      httpMock.verify();
    });
  });

  describe('#getProduct', () => {
    it('should return a product', () => {
      const id = '100';
      const product = { name: 'Product1', price: 100 };

      service.getProduct(id).subscribe(data => {
        expect(data).toEqual(product);
      });

      const req = httpMock.expectOne(service.baseURL + 'products/' + id);
      expect(req.request.method).toBe('GET');
      req.flush(product);
      httpMock.verify();
    });
  });

  describe('#createProduct', () => {
    it('should return a product', () => {
      const product = { name: 'Product1', price: 100 };

      service.createProduct(product).subscribe(data => {
        expect(data.name).toEqual(product.name);
      });

      const req = httpMock.expectOne(service.baseURL + 'products');
      expect(req.request.method).toBe('POST');
      req.flush(product);
      httpMock.verify();
    });
  });

  describe('#updateProduct', () => {
    it('should return a product', () => {
      const id = '100';
      const product = { name: 'Product1', price: 100 };

      service.updateProduct(id, product).subscribe(data => {
        expect(data.name).toEqual(product.name);
      });

      const req = httpMock.expectOne(service.baseURL + 'products/' + id);
      expect(req.request.method).toBe('PUT');
      req.flush(product);
      httpMock.verify();
    });
  });

  describe('#deleteProduct', () => {
    it('test delete product', () => {
      const id = '100';

      service.deleteProduct(id).subscribe();

      const req = httpMock.expectOne(service.baseURL + 'products/' + id);
      expect(req.request.method).toBe('DELETE');
      req.flush({});
      httpMock.verify();
    });
  });

});
