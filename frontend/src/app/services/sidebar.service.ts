import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SidebarService {
  
  sideBarSignal = signal(false);

  onMenuClick() {
    this.sideBarSignal.set(!this.sideBarSignal());
  }
}
