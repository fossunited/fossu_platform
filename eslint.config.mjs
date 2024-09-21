import globals from 'globals'
import pluginJs from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import prettierConfig from 'eslint-config-prettier'
import prettierPlugin from 'eslint-plugin-prettier'

export default [
  {
    ignores: [
      '**/node_modules/**',
      'fossunited/public/dist/**/*',
      'fossunited/public/dashboard/**/*',
    ],
  },
  { files: ['**/*.{js,mjs,cjs,vue}'] },
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        Razorpay: 'readonly',
        frappe: 'readonly',
        Vue: 'readonly',
        SetVueGlobals: 'readonly',
        __: 'readonly',
        repl: 'readonly',
        Class: 'readonly',
        locals: 'readonly',
        cint: 'readonly',
        cstr: 'readonly',
        cur_frm: 'readonly',
        cur_dialog: 'readonly',
        cur_page: 'readonly',
        cur_list: 'readonly',
        cur_tree: 'readonly',
        msg_dialog: 'readonly',
        is_null: 'readonly',
        in_list: 'readonly',
        has_common: 'readonly',
        posthog: 'readonly',
        has_words: 'readonly',
        validate_email: 'readonly',
        open_web_template_values_editor: 'readonly',
        validate_name: 'readonly',
        validate_phone: 'readonly',
        validate_url: 'readonly',
        get_number_format: 'readonly',
        format_number: 'readonly',
        format_currency: 'readonly',
        comment_when: 'readonly',
        open_url_post: 'readonly',
        toTitle: 'readonly',
        lstrip: 'readonly',
        rstrip: 'readonly',
        strip: 'readonly',
        strip_html: 'readonly',
        replace_all: 'readonly',
        flt: 'readonly',
        precision: 'readonly',
        CREATE: 'readonly',
        AMEND: 'readonly',
        CANCEL: 'readonly',
        copy_dict: 'readonly',
        get_number_format_info: 'readonly',
        strip_number_groups: 'readonly',
        print_table: 'readonly',
        Layout: 'readonly',
        web_form_settings: 'readonly',
        $c: 'readonly',
        $a: 'readonly',
        $i: 'readonly',
        $bg: 'readonly',
        $y: 'readonly',
        $c_obj: 'readonly',
        refresh_many: 'readonly',
        refresh_field: 'readonly',
        toggle_field: 'readonly',
        get_field_obj: 'readonly',
        get_query_params: 'readonly',
        unhide_field: 'readonly',
        hide_field: 'readonly',
        set_field_options: 'readonly',
        getCookie: 'readonly',
        getCookies: 'readonly',
        get_url_arg: 'readonly',
        md5: 'readonly',
        $: 'readonly',
        jQuery: 'readonly',
        moment: 'readonly',
        hljs: 'readonly',
        Awesomplete: 'readonly',
        Sortable: 'readonly',
        Showdown: 'readonly',
        Taggle: 'readonly',
        Gantt: 'readonly',
        Slick: 'readonly',
        Webcam: 'readonly',
        PhotoSwipe: 'readonly',
        PhotoSwipeUI_Default: 'readonly',
        io: 'readonly',
        JsBarcode: 'readonly',
        L: 'readonly',
        Chart: 'readonly',
        DataTable: 'readonly',
        Cypress: 'readonly',
        cy: 'readonly',
        it: 'readonly',
        describe: 'readonly',
        expect: 'readonly',
        context: 'readonly',
        before: 'readonly',
        beforeEach: 'readonly',
        after: 'readonly',
        qz: 'readonly',
        localforage: 'readonly',
        extend_cscript: 'readonly',
      },
      parserOptions: { sourceType: 'module' },
    },
  },
  pluginJs.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  prettierConfig, // Disables ESLint rules that conflict with Prettier
  {
    rules: {
      'prettier/prettier': 'error',
      indent: 'off',
      'brace-style': 'off',
      'no-mixed-spaces-and-tabs': 'off',
      'no-useless-escape': 'off',
      'space-unary-ops': ['error', { words: true }],
      'linebreak-style': 'off',
      quotes: 'off',
      semi: 'off',
      camelcase: 'off',
      'no-unused-vars': 'off',
      'no-console': ['warn'],
      'no-extra-boolean-cast': 'off',
      'no-control-regex': 'off',
      'vue/multi-word-component-names': 'off', // Disable the multi-word component names rule
      'vue/no-reserved-component-names': 'off', // Disable the no-reserved-component-names. This is done because frappe-ui uses names such as "Input" & "Button" for its components.
      'vue/no-v-html': 'off',
    },
    plugins: {
      prettier: prettierPlugin,
    },
  },
]
