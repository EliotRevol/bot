import argparse
import os
from urllib.parse import unquote
import sys

sys.path.append("../")
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
from core.src.bot import runJob
from core.src.export import save_json, save_csv
from core.src.user_agent_generator import generate_user_agent_and_resolution

events =  ['{"type": "watchOne", "video_id": "mw4L2xmEtS8", "searchTerm":"Jordan Bardella face à Pascal Praud : Drame de Crépol, traitement médiatique, vie privée... ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "wzGgpUSi6sU", "searchTerm":" Quel président ? François-Xavier Bellamy répond ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "aDANc6xd3wU", "searchTerm":" L UNION EUROPÉENNE S EST COUCHÉE DEVANT LES LABOS PHARMACEUTIQUES ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "3mbpe-Jl3M", "searchTerm":"Raphaël Glucksmann : On fait la même erreur avec Xi Jinping qu avec Vladimir Poutine", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "HR_UZhz9dwQ", "searchTerm":"Européennes: Bardella a-t-il tué le match ?", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "sJLQbMNkPp8", "searchTerm":"François-Xavier Bellamy :  L erreur du moment est de croire que tout changement est un progrès", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "PEQSgJ4NEuY", "searchTerm":" LA RÉACTION D EMMANUEL MACRON EST CELLE D UN ENFANT G TÉ - Manon Aubry ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "LwNpZ9Lw7Yk", "searchTerm":" Le président chinois Xi Jinping en France : Il ne faut pas le traiter en ami", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "oQpryKlWYjY", "searchTerm":"Débat G. Attal / J. Bardella - Replay du 20H de TF1", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "nW6oi4ur4rE", "searchTerm":"Lutte contre l immigration illégale : Un scandale démocratique révoltant", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "8E3yWUz0fRs", "searchTerm":" MÉLENCHON AU SECOND TOUR POUR CHANGER L HISTOIRE ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "bqD5Z0IM4fs", "searchTerm":"La France est à la traîne sur l aide à l Ukraine : l interview en intégralité de Raphaël Glucksmann", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "OY2WvPg35-Y", "searchTerm":"Européennes: le premier débat entre Jordan Bardella et Valérie Hayer en intégralité", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "kFMw-t4uYcY", "searchTerm":"François-Xavier Bellamy à l Université Libé : Le Grand Oral des européennes ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "frUdd1legTM", "searchTerm":" NOUS PROPOSONS UNE ALLOCATION D AUTONOMIE POUR TOUS LES JEUNES ! ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "JrakvQ9n5Ug", "searchTerm":"Raphaël Glucksmann : Le gouvernement Netanyahou n offre aucune perspective aux palestiniens", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "TmIVC9AGTuo", "searchTerm":"Jordan Bardella : L Europe doit mettre fin à une forme de naïveté à l égard de la mondialisation", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "mbYjSCAqJcQ", "searchTerm":"Réponse à Ursula von der Leyen", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "PX0BnQEPYD8", "searchTerm":"GLUCKSMANN CHAHUTÉ, MÉLENCHON ACCUSÉ : IL Y A T-IL « DEUX GAUCHES »IRRÉCONCILIABLES ?", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "OiLbOiHfW4I", "searchTerm":"GAZA, PARIS EST AVEC TOI : AU-DELÀ DE LA POLÉMIQUE GLUCKSMANN, LE VRAI VISAGE DU DÉFILÉ DU 1ER MAI ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "OrPBJyDvp2w", "searchTerm":"L union fait la France !", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "oQ974TmUXmM", "searchTerm":"Loi Avia et application de traçage : « Jamais notre pays ne devrait renoncer aux garanties fondam… ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "8WzJKg3BXO0", "searchTerm":"BARDELLA EST LE LARBIN DES PATRONS ! ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "VI1HuzaPO2k", "searchTerm":"Raphaël Glucksmann, socialiste isolé en Europe - Patrick Cohen - C à vous - 02/05/2024 ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "VjILoreoNco", "searchTerm":"Jordan Bardella IMPLACABLE sur l insécurité ! | Apolline Matin", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "87SjXgwpp28", "searchTerm":"Le Grand Oral de François-Xavier Bellamy - Les Grandes Gueules de RMC ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "bjWQ9bshmXQ", "searchTerm":" MACRON NE PEUT PLUS METTRE UN PIED DEHORS ! ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "mtyWEF0-XlE", "searchTerm":"R.Glucksmann répond à Tom Benoit en direct à propos de l’utilisation de l’épargne privée par l’UE ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "qJ_J4UcECiw", "searchTerm":"🔴 EN DIRECT - Jordan Bardella face aux Grandes Gueules !", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "XINnXJ0UZF0", "searchTerm":"Les élections européennes pourraient BOULEVERSER le quotidien des Français !", "watchTime": 180000}', 
        '{"type": "watchOne", "video_id": "XiYNdoyoLRE", "searchTerm":" MACRON NE POURRA PAS INTERDIRE LA COLERE POPULAIRE ", "watchTime": 180000}',	
        '{"type": "watchOne", "video_id": "pLpa4JY9ovA", "searchTerm":"« Face aux Territoires » avec Raphaël Glucksmann ", "watchTime": 180000}', 		 
        '{"type": "watchOne", "video_id": "70_vcb0EQtk", "searchTerm":"🔴 DIRECT - L intégrale de l interview de Jordan Bardella, président du RN, sur RMC", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "iuzT1FI16nM", "searchTerm":"François-Xavier Bellamy:  Moi, je crois au libre-échange", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "9DEiF0dIhFE", "searchTerm":" LES DRÔLES LEÇONS DE DÉMOCRATIE D ÉLISABETH BORNE, LA PRO DU 49.3 ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "lj64t9DM7Jk", "searchTerm":"Bardella, Glucksmann : les visages souriants de l’anti-macronisme", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "oOdXYFGohf0", "searchTerm":"Jordan Bardella répond à Eric Dupond-Moretti sur le tacle à Marine Le Pen !", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "DWDCO4c5kQg", "searchTerm":" EUROPÉENNES : le programme des Républicains (François-Xavier Bellamy)", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "biizmZH7cEY", "searchTerm":" Manon Aubry:  Au pouvoir, la FI appliquera son programme contre les règles européennes  ", "watchTime": 180000}',
        '{"type": "watchOne", "video_id": "Yz9R8BYMisY", "searchTerm":"« Européennes : bientôt Glucksmann devant Hayer ? ", "watchTime": 180000}',
        '{"type": "fetchAutoplay", "searchSelection": 73, "watchTime": 180000}',
	    ]





out_path = './output/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="output filename")
    parser.add_argument("-c", "--cookie", help="cookies filename")
    args = parser.parse_args()
    ################################################
    # Launch with user agent and screen resolution #
    ################################################
    user_agent_resolution = generate_user_agent_and_resolution()
    res = runJob(events, user_agent_resolution, args.cookie)
    ###################################################
    # Launch without user agent and screen resolution #
    ###################################################
    # res = runJob(events,None,None,None)
    for elem in res:
        print(unquote(elem['title']))
    print(res)
    save_json(res, args.filename)
    save_csv(res, args.filename)
    # run_bot(events, out_path, args.filename)

    #################################
    # Get 4 random youtube video id #
    #################################
    # print(get_randoms_videos(4))
