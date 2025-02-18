/*
 * Copyright 2015-2022 Univention GmbH
 *
 * https://www.univention.de/
 *
 * All rights reserved.
 *
 * The source code of this program is made available
 * under the terms of the GNU Affero General Public License version 3
 * (GNU AGPL V3) as published by the Free Software Foundation.
 *
 * Binary versions of this program provided by Univention to you as
 * well as other copyrighted, protected or trademarked materials like
 * Logos, graphics, fonts, specific documentations and configurations,
 * cryptographic keys etc. are subject to a license agreement between
 * you and Univention and not subject to the GNU AGPL V3.
 *
 * In the case you use this program under the terms of the GNU AGPL V3,
 * the program is provided in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License with the Debian GNU/Linux or Univention distribution in file
 * /usr/share/common-licenses/AGPL-3; if not, see
 * <https://www.gnu.org/licenses/>.
 */
/*global define*/

define([
	"dojo/_base/lang",
	"dojo/on",
	"dojo/keys",
	"dojo/dom",
	"dojo/json",
	"dojo/Deferred",
	"dojo/request/xhr",
	"dojox/html/entities",
	"put-selector/put",
	"login",
	"umc/tools",
	"umc/dialog",
	"umc/widgets/Button",
	"./TextBox",
	"./PasswordBox",
	"./lib",
	"umc/i18n/tools",
	"umc/i18n!."
], function(lang, on, keys, dom, json, Deferred, xhr, entities, put, login, tools, dialog, Button, TextBox, PasswordBox, lib, i18nTools, _) {

	return {
		hash: 'passwordchange',
		enabledViaUcr: 'umc/self-service/passwordchange/frontend/enabled',
		visible: true,

		title: _('Password change'),
		desc: _('Change your (expired) password.'),
		contentContainer: null,
		steps: null,
		startup: function() {
			if (this._username.value !== '') {
				this._oldPassword.focus();
			} else {
				this._username.focus();
			}
		},

		/**
		 * Returns the title of the subpage.
		 * */
		getTitle: function() {
			var locale = i18nTools.defaultLang().slice(0, 2);
			var ucrTitleKey = "umc/self-service/" + this.hash + "/title/" + locale;
			var ucrTitleKeyEnglish = "umc/self-service/" + this.hash + "/title/en";
			return tools.status(ucrTitleKey) || tools.status(ucrTitleKeyEnglish) || this.title;
		},

		/**
		 * Returns the description of the subpage.
		 * */
		getDesc: function() {
			return _(this.desc);
		},

		/**
		 * Return the content node of the subpage.
		 * If the content does not exists, it will be generated.
		 * */
		getContent: function() {
			if (!this.contentContainer) {
				this.contentContainer = put('div.contentWrapper');
				put(this.contentContainer, 'h2', this.getTitle());
				put(this.contentContainer, 'div.contentDesc', this.getDesc());
				put(this.contentContainer, this._getSteps());
			}
			return this.contentContainer;
		},

		/**
		 * Return the steps for the content node.
		 * If the steps do not exists, they will be generated.
		 * Note: Please call getContent for generating the steps.
		 * */
		_getSteps: function() {
			if (!this.steps) {
				this.steps = put('ol#PasswordChangeSteps.PasswordOl');
				this._createUsername();
				this._createOldPassword();
				this._createNewPassword();
				this._createSubmit();
			}
			return this.steps;
		},

		/**
		 * Creates input field for username.
		 * */
		_createUsername: function() {
			var step = put('li.step');
			var label = put('div.stepLabel', _('Username'));
			put(step, label);
			this._username = new TextBox({
				'class': 'soloLabelPane',
				isValid: function() {
					return !!this.get('value');
				},
				required: true
			});
			this._username.startup();
			login.onInitialLogin(lang.hitch(this, function(username) {
				this._username.set('value', tools.status('username'));
				this._username.set('disabled', true);
			}));
			put(step, this._username.domNode);
			put(this.steps, step);
		},

		/**
		 * Creates input field for old password.
		 * */
		_createOldPassword: function() {
			var step = put('li.step');
			var label = put('div.stepLabel', _('Old Password'));
			put(step, label);
			this._oldPassword = new TextBox({
				'class': 'soloLabelPane',
				type: 'password',
				isValid: function() {
					return !!this.get('value');
				},
				required: true
			});
			this._oldPassword.startup();
			put(step, this._oldPassword.domNode);
			put(this.steps, step);
		},

		/**
		 * Creates input fields for new password.
		 * */
		_createNewPassword: function() {
			var step = put('li.step');
			var label = put('div.stepLabel', _('New Password'));
			put(step, label);
			this._newPassword = new PasswordBox({
				'class': 'soloLabelPane left'
			});
			this._newPassword.startup();
			put(step, this._newPassword.domNode);
			put(this.steps, step);

			step = put('li.step');
			label = put('div.stepLabel', _('New Password (retype)'));
			put(step, label);
			this._verifyPassword = new TextBox({
				type: 'password',
				'class': 'soloLabelPane',
				isValid: lang.hitch(this, function() {
					return this._newPassword.get('value') ===
						this._verifyPassword.get('value');
				}),
				invalidMessage: _('The passwords do not match, please retype again.'),
				required: true
			});
			this._verifyPassword.startup();
			put(step, this._verifyPassword.domNode);
			put(this.steps, step);
		},

		/**
		 * Creates submit button.
		 * */
		_createSubmit: function() {
			var step = put('div.umcPageFooter');
			var buttonsRight = put(step, 'div.umcPageFooterRight');
			this._submitButton = new Button({
				label: _('Change password'),
				onClick: lang.hitch(this, '_setPassword')
			});
			put(buttonsRight, this._submitButton.domNode);

			// let the user submit the form by pressing ENTER
			on(document, "keyup", lang.hitch(this, function(evt) {
				if (evt.keyCode === keys.ENTER && !this._submitButton.get('disabled')) {
					this._setPassword();
				}
			}));
			put(this.steps, step);
		},

		/**
		 * Changes the current password if all input fields are valid.
		 * */
		_setPassword: function() {
			var allInputFieldsAreValid = this._username.isValid() &&
				this._oldPassword.isValid() &&
				this._newPassword.isValid() &&
				this._verifyPassword.isValid();

			if (!allInputFieldsAreValid) {
				return;
			}
			this._submitButton.set('disabled', true);

			var authData = {
				'username': this._username.get('value'),
				'password': this._oldPassword.get('value')
			};
			var authDataPassword = lang.mixin({}, authData, {
				'new_password': this._newPassword.get('value')
			});

			var _changePassword = lang.hitch(this, function() {
				var deferred = new Deferred();
				if (!tools.status('loggedIn')) {
					// not logged in -> issue an authentication request
					tools.umcpCommand('auth', authData, {
						401: function(info) {
							if (info.result && info.result.password_expired) {
								tools.umcpCommand('auth', authDataPassword, { 401: function() {
									// make sure to ignore all kinds of errors (including 401)
								}}).then(function() {
									// cancel deferred to not change password a second time
									deferred.resolve(true);
								}, function(error) {
									deferred.reject(error);
								});
							} else {
								deferred.reject(info);
							}
						}
					}).then(function() {
						deferred.resolve(false);
					}, function(info) {
						if (tools.parseError(info).status != 401) {
							deferred.reject(info);
						}
					});

				} else {
					// already logged in -> return a resolved deferred
					deferred.resolve(false);
				}
				return deferred.then(lang.hitch(this, function(cancel) {
					if (cancel) {
						return true;
					}
					return tools.umcpCommand('set', {
						password: authDataPassword
					}).then(function() {
						// return 'true' to indicate success
						return true;
					});
				}));
			});

			var _handleError = lang.hitch(this, function(err) {
				var info = tools.parseError(err);
				if (info.status === 401 && (!info.result || !info.result.password_change_failed)) {
					// wrong credentials -> display custom error message
					// mask "The authentication has failed, please login again."
					info.message = _('Changing password failed. The username and/or the old password is not correct.');
				}
				dialog.alert(entities.encode(info.message));

				// return 'false' to indicate failure
				return false;
			});

			var _resetForm = lang.hitch(this, function(success) {
				this._oldPassword.reset();
				this._newPassword.reset();
				this._verifyPassword.reset();
				this._submitButton.set('disabled', false);
				return success;
			});

			var _handleRedirect = lang.hitch(this, function(success) {
				var redirectUrl = lib._getUrlForRedirect();
				if (redirectUrl && success) {
					dialog.confirm(entities.encode(_('The password has been changed successfully.')), [{label: _('OK'), name: 'submit'}]).then(function() {
						window.open(redirectUrl, "_self");
					});
				}
			});

			// trigger chain of asynchronous actions
			_changePassword().then(null, _handleError).then(_resetForm).then(_handleRedirect);
		},

		/**
		 * Clears all input field values of the subpage.
		 * */
		_clearAllInputFields: function() {
			this._username.reset();
			this._oldPassword.reset();
			this._newPassword.reset();
			this._verifyPassword.reset();
		}
	};
});
