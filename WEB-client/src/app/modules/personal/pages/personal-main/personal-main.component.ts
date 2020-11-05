import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-personal-main',
  templateUrl: './personal-main.component.html',
  styleUrls: ['./personal-main.component.scss']
})
export class PersonalMainComponent implements OnInit {
  visibility:boolean = true;

  constructor() { }

  ngOnInit(): void {
  }

  onChanged(event: any){
    this.visibility = event;
    console.log(this.visibility)
  }
}
