import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.scss']
})
export class EventPageComponent implements OnInit {
  visibility: boolean = true;

  constructor() { }

  ngOnInit(): void {
  }

  onChanged(event: any){
    this.visibility = event;
    console.log(this.visibility)
  }

}
