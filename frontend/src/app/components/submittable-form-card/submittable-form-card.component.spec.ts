import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmittableFormCardComponent } from './submittable-form-card.component';

describe('SubmittableFormCardComponent', () => {
  let component: SubmittableFormCardComponent;
  let fixture: ComponentFixture<SubmittableFormCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubmittableFormCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubmittableFormCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
