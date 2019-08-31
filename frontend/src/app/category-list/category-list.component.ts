import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-category-list',
  templateUrl: './category-list.component.html',
  styleUrls: ['./category-list.component.css']
})
export class CategoryListComponent implements OnInit {

  categories: [];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.getCategoriesWithProducts();
  }

  getCategoriesWithProducts() {
    return this.api.getCategoriesWithProducts().subscribe((data: []) => {
      this.categories = data;
    });
  }

  deleteCategory(id: string) {
    return this.api.deleteCategory(id).subscribe(() => {
      this.getCategoriesWithProducts();
    });
  }

}
