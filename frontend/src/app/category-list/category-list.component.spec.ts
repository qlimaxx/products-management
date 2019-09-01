import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryListComponent } from './category-list.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ApiService } from '../api.service';

describe('CategoryListComponent', () => {
  let component: CategoryListComponent;
  let fixture: ComponentFixture<CategoryListComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [CategoryListComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(CategoryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should has categories', () => {
    const categories: any = [{ name: 'Category1' }];
    const req = httpMock.expectOne(api.baseURL + 'categories?products=1');
    req.flush(categories);
    expect(component.categories).toEqual(categories);
  });

  it('should get categories after delete', () => {
    const categories1: any = [{ name: 'Category1' }];
    const categories2: any = [{ name: 'Category2' }];
    const req1 = httpMock.expectOne(api.baseURL + 'categories?products=1');
    req1.flush(categories1);
    expect(component.categories).toEqual(categories1);
    component.deleteCategory('id');
    const req2 = httpMock.expectOne(api.baseURL + 'categories/id');
    req2.flush({});
    expect(req2.request.method).toBe('DELETE');
    const req3 = httpMock.expectOne(api.baseURL + 'categories?products=1');
    req3.flush(categories2);
    expect(component.categories).toEqual(categories2);
  });
});
