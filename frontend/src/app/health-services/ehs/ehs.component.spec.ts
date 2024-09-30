import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EhsComponent } from './ehs.component';

describe('EhsComponent', () => {
  let component: EhsComponent;
  let fixture: ComponentFixture<EhsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EhsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EhsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
