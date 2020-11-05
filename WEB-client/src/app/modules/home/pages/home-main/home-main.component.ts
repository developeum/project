import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-main',
  templateUrl: './home-main.component.html',
  styleUrls: ['./home-main.component.scss']
})
export class HomeMainComponent implements OnInit {
  visibility: boolean = true;

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  onClick(){
    this.router.navigate(["/auth"]);
    console.log("button clicked")
  }

  onChanged(event: any){
    this.visibility = event;
    console.log(this.visibility)
  }
}
