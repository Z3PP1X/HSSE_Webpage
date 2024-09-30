import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CallToActionBannerComponent } from './call-to-action-banner.component';

describe('CallToActionBannerComponent', () => {
  let component: CallToActionBannerComponent;
  let fixture: ComponentFixture<CallToActionBannerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CallToActionBannerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CallToActionBannerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
