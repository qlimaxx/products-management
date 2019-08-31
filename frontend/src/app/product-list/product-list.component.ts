import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {

  products: [];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.getProductsWithCategories();
  }

  getProductsWithCategories() {
    return this.api.getProductsWithCategories().subscribe((data: []) => {
      this.products = data;
    });
  }

  deleteProduct(id: string) {
    return this.api.deleteProduct(id).subscribe(() => {
      this.getProductsWithCategories();
    });
  }

}
