import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryEditComponent } from './category-edit.component';
import { FormsModule } from '@angular/forms';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ApiService } from '../api.service';

describe('CategoryEditComponent', () => {
  let component: CategoryEditComponent;
  let fixture: ComponentFixture<CategoryEditComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, HttpClientTestingModule, RouterTestingModule],
      declarations: [CategoryEditComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(CategoryEditComponent);
    component = fixture.componentInstance;
    component.categoryId = 'id';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should has category', () => {
    const category: any = { name: 'Category1' };
    const req = httpMock.expectOne(api.baseURL + 'categories/id');
    req.flush(category);
    expect(component.categoryData).toEqual(category);
  });

  it('edit category', () => {
    const category1: any = { name: 'Category1' };
    const category2: any = { name: 'Category2' };
    const req1 = httpMock.expectOne(api.baseURL + 'categories/id');
    req1.flush(category1);
    expect(component.categoryData).toEqual(category1);
    component.categoryData = category2;
    component.editCategory();
    const req2 = httpMock.expectOne(api.baseURL + 'categories/id');
    expect(req2.request.method).toBe('PUT');
    expect(req2.request.body).toEqual(component.categoryData);
  });
});
