import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductEditComponent } from './product-edit.component';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ApiService } from '../api.service';

describe('ProductEditComponent', () => {
  let component: ProductEditComponent;
  let fixture: ComponentFixture<ProductEditComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, NgSelectModule, HttpClientTestingModule, RouterTestingModule],
      declarations: [ProductEditComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(ProductEditComponent);
    component = fixture.componentInstance;
    component.productId = 'id';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should has product', () => {
    const product: any = { name: 'Product1' };
    const req = httpMock.expectOne(api.baseURL + 'products/id?categories=1');
    req.flush(product);
    expect(component.productData).toEqual(product);
  });

  it('edit product', () => {
    const product1: any = { name: 'Product1', categories: [] };
    const product2: any = { name: 'Product2', categories: [] };
    const categories: any = [{ name: 'Category1' }];
    let req1 = httpMock.expectOne(api.baseURL + 'products/id?categories=1');
    req1.flush(product1);
    expect(component.productData).toEqual(product1);
    req1 = httpMock.expectOne(api.baseURL + 'categories');
    req1.flush(categories);
    component.productData = product2;
    component.editProduct();
    const req2 = httpMock.expectOne(api.baseURL + 'products/id');
    expect(req2.request.method).toBe('PUT');
    expect(req2.request.body).toEqual(product2);
  });
});
