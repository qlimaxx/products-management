import { Component, OnInit, Input } from '@angular/core';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-product-create',
  templateUrl: './product-create.component.html',
  styleUrls: ['./product-create.component.css']
})
export class ProductCreateComponent implements OnInit {

  @Input() productData: any = {};

  categories: Observable<any[]>;
  selectedCategories = [];

  constructor(private api: ApiService, private router: Router) { }

  ngOnInit() {
    this.categories = this.api.getCategories();
  }

  createProduct() {
    this.productData.categories = this.selectedCategories.map(({ uuid }) => uuid);
    this.api.createProduct(this.productData).subscribe(() => {
      this.router.navigate(['/products']);
    });
  }

}
