import {Component, ViewEncapsulation} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';

enum Tab {
  FRONTEND,
  BACKEND
}

@UntilDestroy()
@Component({
  selector: 'app-component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class AppComponent {
  readonly tab = Tab;
  currentTab: number = Tab.FRONTEND;
  
  constructor(
    protected router: Router,
  ) { }

  ngOnInit() {
    this.router.events.pipe(untilDestroyed(this)).subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.setActiveTab();  
      }
    }); 
    this.setActiveTab();
  }

  setActiveTab(): void {
    switch (true) {
      case this.router.url.includes('player-summary'):
        this.currentTab = Tab.FRONTEND;
        break;
      case this.router.url.includes('player-summary-api'):
        this.currentTab = Tab.BACKEND;
        break;
    }
  }

}
