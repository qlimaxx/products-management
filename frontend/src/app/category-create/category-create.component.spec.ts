import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryCreateComponent } from './category-create.component';
import { FormsModule } from '@angular/forms';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ApiService } from '../api.service';

describe('CategoryCreateComponent', () => {
  let component: CategoryCreateComponent;
  let fixture: ComponentFixture<CategoryCreateComponent>;
  let api: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, HttpClientTestingModule, RouterTestingModule],
      declarations: [CategoryCreateComponent],
      providers: [ApiService]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    api = TestBed.get(ApiService);
    httpMock = TestBed.get(HttpTestingController);
    fixture = TestBed.createComponent(CategoryCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should create category', () => {
    component.categoryData = { name: 'Category1' };
    component.createCategory();
    const req = httpMock.expectOne(api.baseURL + 'categories');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(component.categoryData);
  });
});
