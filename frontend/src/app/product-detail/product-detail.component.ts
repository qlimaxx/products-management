import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.css']
})
export class ProductDetailComponent implements OnInit {

  productId = this.activatedRoute.snapshot.params.id;
  product: any;

  constructor(
    private api: ApiService,
    private activatedRoute: ActivatedRoute,
    private router: Router) { }

  ngOnInit() {
    this.api.getProductWithCategories(this.productId).subscribe((data: {}) => {
      this.product = data;
    });
  }

  deleteProduct() {
    return this.api.deleteProduct(this.productId).subscribe(() => {
      this.router.navigate(['/products']);
    });
  }

}
