import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryDetailComponent } from './category-detail.component';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ApiService } from '../api.service';

describe('CategoryDetailComponent', () => {
  let component: CategoryDetailComponent;
  let fixture: ComponentFixture<CategoryDetailComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, NgSelectModule, RouterTestingModule, HttpClientTestingModule],
      declarations: [CategoryDetailComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(CategoryDetailComponent);
    component = fixture.componentInstance;
    component.categoryId = 'id';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should has category', () => {
    const category: any = { name: 'Category1' };
    const req = httpMock.expectOne(api.baseURL + 'categories/id?products=1');
    req.flush(category);
    expect(component.category).toEqual(category);
  });

  it('delete category', () => {
    const category1: any = { name: 'Category1' };
    const req1 = httpMock.expectOne(api.baseURL + 'categories/id?products=1');
    req1.flush(category1);
    expect(component.category).toEqual(category1);
    component.deleteCategory();
    const req2 = httpMock.expectOne(api.baseURL + 'categories/id');
    expect(req2.request.method).toBe('DELETE');
  });
});
