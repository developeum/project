import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventImgComponent } from './event-img.component';

describe('EventImgComponent', () => {
  let component: EventImgComponent;
  let fixture: ComponentFixture<EventImgComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventImgComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventImgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
