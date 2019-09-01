import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseURL = environment.apiURL;

  headers = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'X-API-Key': environment.apiKey
    })
  };

  constructor(private http: HttpClient) { }

  getCategoriesWithProducts(): Observable<any> {
    return this.http.get(this.baseURL + 'categories', {
      params: new HttpParams().set('products', '1'),
      headers: this.headers.headers
    });
  }

  getCategories(): Observable<any> {
    return this.http.get(this.baseURL + 'categories', this.headers);
  }

  getCategoryWithProducts(id: string): Observable<any> {
    return this.http.get(this.baseURL + 'categories/' + id, {
      params: new HttpParams().set('products', '1'),
      headers: this.headers.headers
    });
  }

  getCategory(id: string): Observable<any> {
    return this.http.get(this.baseURL + 'categories/' + id, this.headers);
  }

  createCategory(data: {}): Observable<any> {
    return this.http.post(this.baseURL + 'categories', data, this.headers);
  }

  updateCategory(id: string, data: {}): Observable<any> {
    return this.http.put(this.baseURL + 'categories/' + id, data, this.headers);
  }

  deleteCategory(id: string): Observable<any> {
    return this.http.delete(this.baseURL + 'categories/' + id, this.headers);
  }

  getProductsWithCategories(): Observable<any> {
    return this.http.get(this.baseURL + 'products', {
      params: new HttpParams().set('categories', '1'),
      headers: this.headers.headers
    });
  }

  getProducts(): Observable<any> {
    return this.http.get(this.baseURL + 'products', this.headers);
  }

  getProductWithCategories(id: string): Observable<any> {
    return this.http.get(this.baseURL + 'products/' + id, {
      params: new HttpParams().set('categories', '1'),
      headers: this.headers.headers
    });
  }

  getProduct(id: string): Observable<any> {
    return this.http.get(this.baseURL + 'products/' + id, this.headers);
  }

  createProduct(data: {}): Observable<any> {
    return this.http.post(this.baseURL + 'products', data, this.headers);
  }

  updateProduct(id: string, data: {}): Observable<any> {
    return this.http.put(this.baseURL + 'products/' + id, data, this.headers);
  }

  deleteProduct(id: string): Observable<any> {
    return this.http.delete(this.baseURL + 'products/' + id, this.headers);
  }

}
