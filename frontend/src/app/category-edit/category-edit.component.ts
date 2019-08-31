import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-category-edit',
  templateUrl: './category-edit.component.html',
  styleUrls: ['./category-edit.component.css']
})
export class CategoryEditComponent implements OnInit {

  categoryId = this.activatedRoute.snapshot.params.id;
  categoryData: any = {};

  constructor(
    private api: ApiService,
    private activatedRoute: ActivatedRoute,
    private router: Router) { }

  ngOnInit() {
    this.api.getCategory(this.categoryId).subscribe((data) => {
      this.categoryData = data;
    });
  }

  editCategory() {
    this.api.updateCategory(this.categoryId, this.categoryData).subscribe(() => {
      this.router.navigate(['categories/' + this.categoryId]);
    });
  }

}
