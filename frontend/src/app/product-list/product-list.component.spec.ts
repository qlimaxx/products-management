import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductListComponent } from './product-list.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ApiService } from '../api.service';

describe('ProductListComponent', () => {
  let component: ProductListComponent;
  let fixture: ComponentFixture<ProductListComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [ProductListComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(ProductListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should has products', () => {
    const products: any = [{ name: 'Product1' }];
    const req = httpMock.expectOne(api.baseURL + 'products?categories=1');
    req.flush(products);
    expect(component.products).toEqual(products);
  });

  it('should get products after delete', () => {
    const products1: any = [{ name: 'Product1' }];
    const products2: any = [{ name: 'Product2' }];
    const req1 = httpMock.expectOne(api.baseURL + 'products?categories=1');
    req1.flush(products1);
    expect(component.products).toEqual(products1);
    component.deleteProduct('id');
    const req2 = httpMock.expectOne(api.baseURL + 'products/id');
    req2.flush({});
    expect(req2.request.method).toBe('DELETE');
    const req3 = httpMock.expectOne(api.baseURL + 'products?categories=1');
    req3.flush(products2);
    expect(component.products).toEqual(products2);
  });
});
