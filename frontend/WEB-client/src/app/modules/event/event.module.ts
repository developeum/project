import { GeneralModule } from './../../layout/components/general.module';
import { EventRoutingModule } from './event-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EventPageComponent } from './pages/event-page/event-page.component';
import { EventDataComponent } from './components/event-data/event-data.component';



@NgModule({
  declarations: [EventPageComponent, EventDataComponent],
  imports: [
    CommonModule,
    EventRoutingModule,
    GeneralModule
  ]
})
export class EventModule { }
