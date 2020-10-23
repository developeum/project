import { Event } from './../../../../models/event';
import { EventService } from './../../services/event.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-event-data',
  templateUrl: './event-data.component.html',
  styleUrls: ['./event-data.component.scss']
})
export class EventDataComponent implements OnInit {

  imgToShow: any;
  isImageLoading: boolean = false;
  eventId: number;
  currentEvent: Event;

  constructor(private pageService: EventService) { }

  ngOnInit(): void {
    this.loadEventInfo();
  }

  loadEventInfo(){
    this.pageService.getEventData(this.eventId)
    .subscribe(x => {
      this.currentEvent = x;
      this.loadImg(x.logo_path);
    })
  }

  onClick(){
    if(localStorage.getItem("currentUser") != null){
      this.pageService.postToVisited(this.eventId)
    }
  }

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imgToShow = reader.result;
    }, false);
    if(image){
      reader.readAsDataURL(image)
    }
  }

  loadImg(url: string) {
    this.isImageLoading = true;
    this.pageService.getEventImg(url).subscribe(data => {
      this.createImgFromBlob(data);
      this.isImageLoading = false;
    }, error => {
      this.isImageLoading = false;
      console.log(error)
    })
  }
}
