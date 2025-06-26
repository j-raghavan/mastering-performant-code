/**
 * Button Component
 * 
 * Reusable button component with different styles and states
 */

class Button {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            text: 'Button',
            type: 'primary', // primary, secondary, success, danger, warning
            size: 'medium', // small, medium, large
            disabled: false,
            loading: false,
            icon: null,
            onClick: null,
            ...options
        };

        this.isInitialized = false;
        this.init();
    }

    init() {
        this.createButton();
        this.bindEvents();
        this.isInitialized = true;
    }

    createButton() {
        const buttonClasses = [
            'btn',
            `btn-${this.options.type}`,
            `btn-${this.options.size}`
        ];

        if (this.options.disabled) {
            buttonClasses.push('btn-disabled');
        }

        if (this.options.loading) {
            buttonClasses.push('btn-loading');
        }

        this.container.innerHTML = `
            <button class="${buttonClasses.join(' ')}" ${this.options.disabled ? 'disabled' : ''}>
                ${this.options.loading ? '<span class="btn-spinner"></span>' : ''}
                ${this.options.icon ? `<span class="btn-icon">${this.options.icon}</span>` : ''}
                <span class="btn-text">${this.options.text}</span>
            </button>
        `;

        this.button = this.container.querySelector('button');
    }

    bindEvents() {
        if (this.options.onClick && !this.options.disabled) {
            this.button.addEventListener('click', (e) => {
                e.preventDefault();
                this.options.onClick(e);
            });
        }
    }

    setText(text) {
        this.options.text = text;
        const textElement = this.button.querySelector('.btn-text');
        if (textElement) {
            textElement.textContent = text;
        }
    }

    setDisabled(disabled) {
        this.options.disabled = disabled;
        this.button.disabled = disabled;
        this.button.classList.toggle('btn-disabled', disabled);
    }

    setLoading(loading) {
        this.options.loading = loading;
        this.button.classList.toggle('btn-loading', loading);

        const spinner = this.button.querySelector('.btn-spinner');
        if (loading && !spinner) {
            const spinnerElement = document.createElement('span');
            spinnerElement.className = 'btn-spinner';
            this.button.insertBefore(spinnerElement, this.button.firstChild);
        } else if (!loading && spinner) {
            spinner.remove();
        }
    }

    setType(type) {
        this.options.type = type;
        this.button.className = this.button.className.replace(/btn-\w+/, `btn-${type}`);
    }

    setSize(size) {
        this.options.size = size;
        this.button.className = this.button.className.replace(/btn-\w+/, `btn-${size}`);
    }

    destroy() {
        this.button.removeEventListener('click', this.options.onClick);
        this.container.innerHTML = '';
        this.isInitialized = false;
    }
}

export { Button }; 