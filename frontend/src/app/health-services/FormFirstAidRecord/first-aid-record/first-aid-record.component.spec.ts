import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirstAidRecordComponent } from './first-aid-record.component';

describe('FirstAidRecordComponent', () => {
  let component: FirstAidRecordComponent;
  let fixture: ComponentFixture<FirstAidRecordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FirstAidRecordComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FirstAidRecordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
