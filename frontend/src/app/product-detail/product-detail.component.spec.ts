import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductDetailComponent } from './product-detail.component';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ApiService } from '../api.service';

describe('ProductDetailComponent', () => {
  let component: ProductDetailComponent;
  let fixture: ComponentFixture<ProductDetailComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, NgSelectModule, RouterTestingModule, HttpClientTestingModule],
      declarations: [ProductDetailComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(ProductDetailComponent);
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
    expect(component.product).toEqual(product);
  });

  it('delete product', () => {
    const product1: any = { name: 'Product1' };
    const req1 = httpMock.expectOne(api.baseURL + 'products/id?categories=1');
    req1.flush(product1);
    expect(component.product).toEqual(product1);
    component.deleteProduct();
    const req2 = httpMock.expectOne(api.baseURL + 'products/id');
    expect(req2.request.method).toBe('DELETE');
  });
});
