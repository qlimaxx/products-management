import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-product-edit',
  templateUrl: './product-edit.component.html',
  styleUrls: ['./product-edit.component.css']
})
export class ProductEditComponent implements OnInit {

  productId = this.activatedRoute.snapshot.params.id;
  productData: any = {};
  categories: Observable<any[]>;
  selectedCategories = [];

  constructor(
    private api: ApiService,
    private activatedRoute: ActivatedRoute,
    private router: Router) { }

  ngOnInit() {
    this.api.getProductWithCategories(this.productId).subscribe((data) => {
      this.productData = data;
      this.selectedCategories = data.categories;
    });
    this.categories = this.api.getCategories();
  }

  editProduct() {
    this.productData.categories = this.selectedCategories.map(({ uuid }) => uuid);
    this.api.updateProduct(this.productId, this.productData).subscribe(() => {
      this.router.navigate(['products/' + this.productId]);
    });
  }

}
