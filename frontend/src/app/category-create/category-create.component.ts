import { Component, OnInit, Input } from '@angular/core';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-category-create',
  templateUrl: './category-create.component.html',
  styleUrls: ['./category-create.component.css']
})
export class CategoryCreateComponent implements OnInit {

  @Input() categoryData = {};

  constructor(private api: ApiService, private router: Router) { }

  ngOnInit() {
  }

  createCategory() {
    this.api.createCategory(this.categoryData).subscribe(() => {
      this.router.navigate(['/categories']);
    });
  }

}
