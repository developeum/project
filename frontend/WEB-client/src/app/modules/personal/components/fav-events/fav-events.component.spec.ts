import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavEventsComponent } from './fav-events.component';

describe('FavEventsComponent', () => {
  let component: FavEventsComponent;
  let fixture: ComponentFixture<FavEventsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavEventsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavEventsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
