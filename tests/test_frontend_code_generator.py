"""
Tests for FrontendCodeGenerator agent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.frontend_code_generator import FrontendCodeGenerator


class TestFrontendCodeGenerator:
    """Test suite for FrontendCodeGenerator"""
    
    @pytest.fixture
    def generator(self, environment_vars):
        """Create FrontendCodeGenerator instance for testing"""
        with patch('app.agents.frontend_code_generator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return FrontendCodeGenerator()
    
    @pytest.mark.unit
    def test_init(self, generator):
        """Test FrontendCodeGenerator initialization"""
        assert generator is not None
        assert hasattr(generator, 'component_designer_agent')
        assert hasattr(generator, 'service_developer_agent')
        assert hasattr(generator, 'ui_implementation_agent')
        assert hasattr(generator, 'state_management_agent')
        assert hasattr(generator, 'frontend_coordinator_agent')
    
    @pytest.mark.unit
    def test_system_messages(self, generator):
        """Test that all Angular agent system messages are properly defined"""
        messages = {
            'component_designer': generator._get_component_designer_system_message(),
            'service_developer': generator._get_service_developer_system_message(),
            'ui_implementation': generator._get_ui_implementation_system_message(),
            'state_management': generator._get_state_management_system_message(),
            'frontend_coordinator': generator._get_frontend_coordinator_system_message()
        }
        
        for agent_name, message in messages.items():
            assert len(message) > 100, f"{agent_name} message too short"
            assert "RESPONSIBILITIES" in message, f"{agent_name} missing responsibilities"
            assert "CRITICAL GUIDELINES" in message, f"{agent_name} missing guidelines"
            assert "OUTPUT FORMAT" in message, f"{agent_name} missing output format"
    
    @pytest.mark.unit
    def test_component_designer_message_content(self, generator):
        """Test ComponentDesigner system message contains Angular-specific elements"""
        message = generator._get_component_designer_system_message()
        
        required_terms = [
            "ComponentDesignerAgent", "Angular", "TypeScript", "component", 
            "lifecycle", "OnInit", "Input", "Output", "EventEmitter"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_service_developer_message_content(self, generator):
        """Test ServiceDeveloper system message contains Angular service elements"""
        message = generator._get_service_developer_system_message()
        
        required_terms = [
            "ServiceDeveloperAgent", "Angular", "HttpClient", "Observable", 
            "RxJS", "Injectable", "dependency injection", "HTTP"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_ui_implementation_message_content(self, generator):
        """Test UIImplementation system message contains template/styling elements"""
        message = generator._get_ui_implementation_system_message()
        
        required_terms = [
            "UIImplementationAgent", "Angular", "template", "HTML", "SCSS", 
            "Angular Material", "responsive", "accessibility"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_state_management_message_content(self, generator):
        """Test StateManagement system message contains NgRx elements"""
        message = generator._get_state_management_system_message()
        
        required_terms = [
            "StateManagementAgent", "NgRx", "actions", "reducers", "effects", 
            "selectors", "state", "reactive"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_frontend_code_success(self, generator, sample_frontend_srd):
        """Test successful Angular frontend code generation"""
        with patch('app.agents.frontend_code_generator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock Angular code generation conversation
            mock_messages = [
                Mock(content="""
// app.component.ts
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Task Management App';
}
```
""", source="ComponentDesignerAgent"),
                Mock(content="""
// user.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}
  
  getUsers(): Observable<any[]> {
    return this.http.get<any[]>('/api/users');
  }
}
```
""", source="ServiceDeveloperAgent"),
                Mock(content="""
<!-- app.component.html -->
```html
<div class="app-container">
  <mat-toolbar color="primary">
    <span>{{title}}</span>
  </mat-toolbar>
  <router-outlet></router-outlet>
</div>
```

/* app.component.scss */
```scss
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
```
""", source="UIImplementationAgent"),
                Mock(content="""
// package.json
```json
{
  "name": "angular-app",
  "version": "1.0.0",
  "dependencies": {
    "@angular/core": "^16.0.0",
    "@angular/material": "^16.0.0"
  }
}
```
""", source="FrontendCoordinatorAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            result = await generator.generate_frontend_code(sample_frontend_srd, "test_angular_project")
            
            assert result is not None
            assert isinstance(result, dict)
            assert len(result) > 0
            
            # Check that Angular files were generated
            ts_files = [f for f in result.keys() if f.endswith('.ts')]
            html_files = [f for f in result.keys() if f.endswith('.html')]
            scss_files = [f for f in result.keys() if f.endswith('.scss')]
            json_files = [f for f in result.keys() if f.endswith('.json')]
            
            assert len(ts_files) > 0, "Should generate TypeScript files"
            assert len(html_files) > 0, "Should generate HTML templates"
            assert len(scss_files) > 0, "Should generate SCSS styles"
            assert len(json_files) > 0, "Should generate JSON config files"
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_frontend_code_empty_srd(self, generator):
        """Test Angular code generation with empty SRD"""
        with pytest.raises(ValueError):
            await generator.generate_frontend_code("", "test_project")
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_frontend_code_error_handling(self, generator, sample_frontend_srd):
        """Test error handling in Angular code generation"""
        with patch('app.agents.frontend_code_generator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            mock_instance.run.side_effect = Exception("Test error")
            
            result = await generator.generate_frontend_code(sample_frontend_srd, "test_project")
            
            assert result is not None
            assert "error" in result
    
    @pytest.mark.unit
    def test_extract_generated_angular_code(self, generator):
        """Test Angular code extraction from conversation messages"""
        messages = [
            Mock(content="""
// app.component.ts
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root'
})
export class AppComponent {}
```

<!-- app.component.html -->
```html
<div>Hello Angular</div>
```

/* app.component.scss */
```scss
.container { padding: 1rem; }
```
""", source="TestAgent")
        ]
        
        result = generator._extract_generated_angular_code(messages, "test_project")
        
        assert isinstance(result, dict)
        assert len(result) > 0
        
        # Should extract different file types
        ts_files = [f for f in result.keys() if f.endswith('.ts')]
        html_files = [f for f in result.keys() if f.endswith('.html')]
        scss_files = [f for f in result.keys() if f.endswith('.scss')]
        
        assert len(ts_files) > 0
        assert len(html_files) > 0
        assert len(scss_files) > 0
    
    @pytest.mark.unit
    def test_fallback_angular_structure_creation(self, generator):
        """Test fallback Angular structure when no code is extracted"""
        messages = [Mock(content="No code blocks here", source="TestAgent")]
        
        result = generator._create_fallback_angular_structure(messages, "test_project")
        
        assert isinstance(result, dict)
        assert any("test_project" in path for path in result.keys())
        assert any(path.endswith('.ts') for path in result.keys())
        assert any(path.endswith('.html') for path in result.keys())
        assert any(path.endswith('.scss') for path in result.keys())
        assert any(path.endswith('.json') for path in result.keys())
        
        # Check for Angular-specific files
        assert any('app.module.ts' in path for path in result.keys())
        assert any('app.component.ts' in path for path in result.keys())
        assert any('package.json' in path for path in result.keys())
    
    @pytest.mark.unit
    def test_default_angular_files(self, generator):
        """Test default Angular file generation"""
        app_module = generator._get_default_app_module()
        app_component = generator._get_default_app_component()
        app_template = generator._get_default_app_template()
        package_json = generator._get_default_package_json("test-app")
        
        # App Module should contain Angular imports
        assert "NgModule" in app_module
        assert "BrowserModule" in app_module
        assert "MatToolbarModule" in app_module
        
        # App Component should be valid TypeScript
        assert "@Component" in app_component
        assert "export class AppComponent" in app_component
        
        # Template should contain Angular Material
        assert "mat-toolbar" in app_template
        assert "router-outlet" in app_template
        
        # Package.json should contain Angular dependencies
        assert "@angular/core" in package_json
        assert "@angular/material" in package_json
        assert "test-app" in package_json
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_generated_code(self, generator, temp_output_dir, mock_generated_code):
        """Test saving generated Angular code to disk"""
        # Add Angular-specific files to mock data
        angular_files = {
            **mock_generated_code,
            "src/app/app.component.ts": "Angular component content",
            "src/app/app.component.html": "<div>Angular template</div>",
            "src/app/app.component.scss": ".container { padding: 1rem; }",
            "package.json": '{"name": "angular-app"}'
        }
        
        project_path = await generator.save_generated_code(angular_files, temp_output_dir)
        
        assert project_path is not None
        assert temp_output_dir in project_path


class TestAngularAgentSpecialization:
    """Test Angular agent specialization and focus"""
    
    @pytest.fixture
    def generator(self, environment_vars):
        """Create generator for specialization testing"""
        with patch('app.agents.frontend_code_generator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return FrontendCodeGenerator()
    
    @pytest.mark.unit
    def test_component_designer_specialization(self, generator):
        """Test ComponentDesigner focuses only on components"""
        message = generator._get_component_designer_system_message()
        
        assert "component" in message.lower()
        assert "TypeScript" in message
        assert "Angular" in message
        assert "Do not implement templates" in message or "Focus EXCLUSIVELY on component architecture" in message
    
    @pytest.mark.unit
    def test_service_developer_specialization(self, generator):
        """Test ServiceDeveloper focuses only on services"""
        message = generator._get_service_developer_system_message()
        
        assert "service" in message.lower()
        assert "HttpClient" in message
        assert "Observable" in message
        assert "Do not implement components" in message or "Focus EXCLUSIVELY on services" in message
    
    @pytest.mark.unit
    def test_ui_implementation_specialization(self, generator):
        """Test UIImplementation focuses only on templates/styles"""
        message = generator._get_ui_implementation_system_message()
        
        assert "template" in message.lower()
        assert "HTML" in message
        assert "SCSS" in message
        assert "Do not implement TypeScript logic" in message or "Focus EXCLUSIVELY on templates and styling" in message
    
    @pytest.mark.unit
    def test_state_management_specialization(self, generator):
        """Test StateManagement focuses only on NgRx/state"""
        message = generator._get_state_management_system_message()
        
        assert "state" in message.lower()
        assert "NgRx" in message
        assert "actions" in message.lower()
        assert "Do not implement components" in message or "Focus EXCLUSIVELY on state management" in message
    
    @pytest.mark.unit
    def test_frontend_coordinator_orchestration(self, generator):
        """Test FrontendCoordinator focuses on project coordination"""
        message = generator._get_frontend_coordinator_system_message()
        
        assert "coordinator" in message.lower() or "orchestrat" in message.lower()
        assert "Angular" in message
        assert "project" in message.lower()
        assert "TEAM WORKFLOW" in message


class TestFrontendCodeGeneratorIntegration:
    """Integration tests for FrontendCodeGenerator"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_complete_angular_generation_workflow(self, environment_vars, sample_frontend_srd, temp_output_dir):
        """Test complete Angular code generation workflow"""
        with patch('app.agents.frontend_code_generator.OpenAIChatCompletionClient') as mock_client, \
             patch('app.agents.frontend_code_generator.RoundRobinGroupChat') as mock_chat:
            
            # Setup mocks
            mock_client.return_value = Mock()
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Create comprehensive Angular mock conversation
            mock_messages = [
                # Component Designer output
                Mock(content="""
// src/app/app.component.ts
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Task Management';
}
```

// src/app/auth/login.component.ts
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  
  constructor(private fb: FormBuilder) {}
  
  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }
}
```
""", source="ComponentDesignerAgent"),
                
                # Service Developer output
                Mock(content="""
// src/app/services/auth.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<any>(null);
  
  constructor(private http: HttpClient) {}
  
  login(credentials: any): Observable<any> {
    return this.http.post('/api/auth/login', credentials)
      .pipe(tap(response => {
        localStorage.setItem('token', response.token);
        this.currentUserSubject.next(response.user);
      }));
  }
}
```

// src/app/services/task.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  constructor(private http: HttpClient) {}
  
  getTasks(): Observable<any[]> {
    return this.http.get<any[]>('/api/tasks');
  }
  
  createTask(task: any): Observable<any> {
    return this.http.post<any>('/api/tasks', task);
  }
}
```
""", source="ServiceDeveloperAgent"),
                
                # UI Implementation output
                Mock(content="""
<!-- src/app/app.component.html -->
```html
<mat-toolbar color="primary">
  <span>{{title}}</span>
  <span class="spacer"></span>
  <button mat-button routerLink="/login">Login</button>
</mat-toolbar>

<main class="main-content">
  <router-outlet></router-outlet>
</main>
```

/* src/app/app.component.scss */
```scss
.spacer {
  flex: 1 1 auto;
}

.main-content {
  padding: 2rem;
  min-height: calc(100vh - 64px);
}
```

<!-- src/app/auth/login.component.html -->
```html
<mat-card class="login-card">
  <mat-card-header>
    <mat-card-title>Login</mat-card-title>
  </mat-card-header>
  <mat-card-content>
    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
      <mat-form-field appearance="fill" class="full-width">
        <mat-label>Email</mat-label>
        <input matInput formControlName="email" type="email">
        <mat-error *ngIf="loginForm.get('email')?.hasError('email')">
          Please enter a valid email
        </mat-error>
      </mat-form-field>
      
      <mat-form-field appearance="fill" class="full-width">
        <mat-label>Password</mat-label>
        <input matInput formControlName="password" type="password">
      </mat-form-field>
      
      <button mat-raised-button color="primary" type="submit" 
              [disabled]="loginForm.invalid">
        Login
      </button>
    </form>
  </mat-card-content>
</mat-card>
```
""", source="UIImplementationAgent"),
                
                # State Management output
                Mock(content="""
// src/app/store/auth/auth.actions.ts
```typescript
import { createAction, props } from '@ngrx/store';

export const login = createAction(
  '[Auth] Login',
  props<{ credentials: any }>()
);

export const loginSuccess = createAction(
  '[Auth] Login Success',
  props<{ user: any; token: string }>()
);

export const loginFailure = createAction(
  '[Auth] Login Failure',
  props<{ error: string }>()
);
```

// src/app/store/auth/auth.reducer.ts
```typescript
import { createReducer, on } from '@ngrx/store';
import * as AuthActions from './auth.actions';

export interface AuthState {
  user: any;
  token: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  loading: false,
  error: null
};

export const authReducer = createReducer(
  initialState,
  on(AuthActions.login, state => ({ ...state, loading: true, error: null })),
  on(AuthActions.loginSuccess, (state, { user, token }) => ({
    ...state,
    user,
    token,
    loading: false,
    error: null
  })),
  on(AuthActions.loginFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error
  }))
);
```
""", source="StateManagementAgent"),
                
                # Frontend Coordinator output
                Mock(content="""
// src/app/app.module.ts
```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

import { AppComponent } from './app.component';
import { LoginComponent } from './auth/login.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatToolbarModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

// package.json
```json
{
  "name": "task-management-frontend",
  "version": "1.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "test": "ng test"
  },
  "dependencies": {
    "@angular/animations": "^16.0.0",
    "@angular/cdk": "^16.0.0",
    "@angular/common": "^16.0.0",
    "@angular/compiler": "^16.0.0",
    "@angular/core": "^16.0.0",
    "@angular/forms": "^16.0.0",
    "@angular/material": "^16.0.0",
    "@angular/platform-browser": "^16.0.0",
    "@angular/platform-browser-dynamic": "^16.0.0",
    "@angular/router": "^16.0.0",
    "@ngrx/store": "^16.0.0",
    "@ngrx/effects": "^16.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.13.0"
  }
}
```
""", source="FrontendCoordinatorAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            # Create generator and run complete workflow
            generator = FrontendCodeGenerator()
            
            # Step 1: Generate Angular code
            generated_files = await generator.generate_frontend_code(sample_frontend_srd, "task_management_frontend")
            
            assert generated_files is not None
            assert isinstance(generated_files, dict)
            assert len(generated_files) > 0
            
            # Verify Angular file types
            ts_files = [f for f in generated_files.keys() if f.endswith('.ts')]
            html_files = [f for f in generated_files.keys() if f.endswith('.html')]
            scss_files = [f for f in generated_files.keys() if f.endswith('.scss')]
            json_files = [f for f in generated_files.keys() if f.endswith('.json')]
            
            assert len(ts_files) > 0, "Should generate TypeScript files"
            assert len(html_files) > 0, "Should generate HTML templates"
            assert len(scss_files) > 0, "Should generate SCSS styles"
            assert len(json_files) > 0, "Should generate JSON configuration"
            
            # Step 2: Save code to disk
            project_path = await generator.save_generated_code(generated_files, temp_output_dir)
            
            assert project_path is not None
            assert temp_output_dir in project_path
            
            # Verify Angular-specific content
            angular_module_files = [f for f in generated_files.keys() if 'app.module.ts' in f]
            if angular_module_files:
                module_content = generated_files[angular_module_files[0]]
                assert "NgModule" in module_content
                assert "@angular" in module_content
                
            component_files = [f for f in generated_files.keys() if 'component.ts' in f]
            if component_files:
                component_content = generated_files[component_files[0]]
                assert "@Component" in component_content
                assert "export class" in component_content