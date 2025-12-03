import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="app-container">
      <mat-toolbar color="primary" class="toolbar">
        <mat-icon class="toolbar-icon">trending_up</mat-icon>
        <span class="toolbar-title">Asset Recommendation System</span>
      </mat-toolbar>
      <div class="content-wrapper">
        <app-recommendations></app-recommendations>
      </div>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .toolbar {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      padding: 0 24px;
      height: 64px;
      display: flex;
      align-items: center;
    }

    .toolbar-icon {
      margin-right: 12px;
      font-size: 28px;
      width: 28px;
      height: 28px;
    }

    .toolbar-title {
      font-size: 20px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    .content-wrapper {
      flex: 1;
      padding: 24px;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }

    @media (max-width: 768px) {
      .content-wrapper {
        padding: 16px;
      }

      .toolbar {
        height: 56px;
        padding: 0 16px;
      }

      .toolbar-title {
        font-size: 18px;
      }
    }
  `]
})
export class AppComponent {
  title = 'asset-recommendation-ui';
}

