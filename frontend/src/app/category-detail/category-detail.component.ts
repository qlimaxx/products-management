import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-category-detail',
  templateUrl: './category-detail.component.html',
  styleUrls: ['./category-detail.component.css']
})
export class CategoryDetailComponent implements OnInit {

  categoryId = this.activatedRoute.snapshot.params.id;
  category: any;

  constructor(
    private api: ApiService,
    private activatedRoute: ActivatedRoute,
    private router: Router) { }

  ngOnInit() {
    this.api.getCategoryWithProducts(this.categoryId).subscribe((data: {}) => {
      this.category = data;
    });
  }

  deleteCategory() {
    return this.api.deleteCategory(this.categoryId).subscribe(() => {
      this.router.navigate(['/categories']);
    });
  }

}
